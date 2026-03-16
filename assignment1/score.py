import json
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import serial
from serial.tools import list_ports


scores_lock = threading.Lock()
scores = {}

HTML_PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Micro:bit Scoreboard</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f6f4ef;
      --card: #fffdf8;
      --ink: #1f2933;
      --accent: #b23a48;
      --line: #d9d2c3;
    }
    body {
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      background: linear-gradient(180deg, #f2ede2 0%, #fbfaf6 100%);
      color: var(--ink);
    }
    main {
      max-width: 960px;
      margin: 0 auto;
      padding: 32px 20px 48px;
    }
    h1 {
      margin: 0 0 8px;
      font-size: 2.2rem;
    }
    p {
      margin: 0 0 20px;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 20px;
    }
    .card {
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 16px;
      padding: 18px;
      box-shadow: 0 12px 30px rgba(31, 41, 51, 0.08);
    }
    table {
      width: 100%;
      border-collapse: collapse;
    }
    th, td {
      text-align: left;
      padding: 10px 8px;
      border-bottom: 1px solid var(--line);
      font-size: 0.98rem;
    }
    th {
      font-size: 0.82rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: #5f6c7b;
    }
    td.score {
      font-weight: 700;
      color: var(--accent);
    }
    .empty {
      color: #7b8794;
      font-style: italic;
    }
  </style>
</head>
<body>
  <main>
    <h1>Micro:bit Scoreboard</h1>
    <p id="status">Waiting for scores...</p>
    <div class="grid">
      <section class="card">
        <h2>Live Scores</h2>
        <table>
          <thead>
            <tr>
              <th>Device</th>
              <th>Player</th>
              <th>Score</th>
            </tr>
          </thead>
          <tbody id="live-body"></tbody>
        </table>
      </section>
      <section class="card">
        <h2>Final Scores</h2>
        <table>
          <thead>
            <tr>
              <th>Device</th>
              <th>Player</th>
              <th>Final</th>
            </tr>
          </thead>
          <tbody id="final-body"></tbody>
        </table>
      </section>
    </div>
  </main>
  <script>
    function escapeHtml(value) {
      return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
    }

    function renderRows(rows, emptyText) {
      if (!rows.length) {
        return '<tr><td colspan="3" class="empty">' + emptyText + '</td></tr>';
      }

      return rows.map(function (row) {
        return (
          "<tr>" +
          "<td>" + escapeHtml(row.device_name) + "</td>" +
          "<td>" + escapeHtml(row.player_name) + "</td>" +
          '<td class="score">' + escapeHtml(row.score) + "</td>" +
          "</tr>"
        );
      }).join("");
    }

    async function refreshScores() {
      const status = document.getElementById("status");

      try {
        const response = await fetch("/scores", { cache: "no-store" });
        const data = await response.json();

        document.getElementById("live-body").innerHTML = renderRows(
          data.live_scores,
          "No live scores yet"
        );
        document.getElementById("final-body").innerHTML = renderRows(
          data.final_scores,
          "No final scores yet"
        );
        status.textContent = "Last updated " + new Date().toLocaleTimeString();
      } catch (error) {
        status.textContent = "Unable to load scoreboard right now";
      }
    }

    refreshScores();
    setInterval(refreshScores, 500);
  </script>
</body>
</html>
"""


def resolve_com_port():
    if len(sys.argv) > 1:
        return sys.argv[1]

    candidate_ports = []
    for port in list_ports.comports():
        device = port.device or ""
        description = (port.description or "").lower()
        hwid = (port.hwid or "").lower()

        if (
            "arduino" in description
            or "usb" in description
            or "acm" in device.lower()
            or "usb" in hwid
        ):
            candidate_ports.insert(0, device)
        else:
            candidate_ports.append(device)

    for port in candidate_ports:
        try:
            test_serial = serial.Serial(port=port, baudrate=9600, timeout=0.1)
            test_serial.close()
            return port
        except serial.SerialException:
            continue

    raise serial.SerialException(
        "No usable serial port found. Pass the port explicitly, for example: python score.py /dev/ttyACM0"
    )


def resolve_web_port():
    if len(sys.argv) > 2:
        return int(sys.argv[2])
    return 8000


def parse_score_message(message):
    parts = message.split("|")
    if len(parts) == 3:
        device_name, player_name, score_text = parts
        return {
            "device_name": device_name,
            "player_name": player_name,
            "score": int(score_text),
            "final": False,
        }

    if len(parts) == 4 and parts[0] == "END":
        _, device_name, player_name, score_text = parts
        return {
            "device_name": device_name,
            "player_name": player_name,
            "score": int(score_text),
            "final": True,
        }

    return None


def update_scores(message):
    parsed = parse_score_message(message)
    if parsed is None:
        return

    with scores_lock:
        scores[parsed["device_name"]] = parsed


def build_snapshot():
    with scores_lock:
        live_scores = []
        final_scores = []

        for score in scores.values():
            if score["final"]:
                final_scores.append(score.copy())
            else:
                live_scores.append(score.copy())

    live_scores.sort(key=lambda item: (-item["score"], item["player_name"], item["device_name"]))
    final_scores.sort(key=lambda item: (-item["score"], item["player_name"], item["device_name"]))

    return {
        "live_scores": live_scores,
        "final_scores": final_scores,
    }


def serial_reader_loop(ser):
    while True:
        if ser.in_waiting > 0:
            msg = ser.readline()
            line = msg.decode("utf-8", errors="replace").strip()

            if line:
                print(line)
                try:
                    update_scores(line)
                except ValueError:
                    print(f"Ignored malformed score line: {line}")
        else:
            time.sleep(0.05)


class ScoreRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            body = HTML_PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if self.path == "/scores":
            body = json.dumps(build_snapshot()).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        return


def main():
    com_port = resolve_com_port()
    web_port = resolve_web_port()
    ser = serial.Serial(port=com_port, baudrate=9600, timeout=0.1)

    print(f"Listening for scores on {com_port}")
    print(f"Dashboard available at http://127.0.0.1:{web_port}")

    reader_thread = threading.Thread(target=serial_reader_loop, args=(ser,), daemon=True)
    reader_thread.start()

    server = ThreadingHTTPServer(("0.0.0.0", web_port), ScoreRequestHandler)

    try:
        server.serve_forever()
    finally:
        server.server_close()
        ser.close()


if __name__ == "__main__":
    try:
        main()
    except serial.SerialException as err:
        print(f"SerialException: {err}")
    except KeyboardInterrupt:
        print("Program terminated!")
