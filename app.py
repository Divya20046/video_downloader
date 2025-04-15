from flask import Flask, render_template, request, send_from_directory
import os
from yt_dlp import YoutubeDL

app = Flask(__name__)
DOWNLOAD_FOLDER = os.path.join('static', 'downloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
app.config['FLASK_ENV'] = os.getenv('FLASK_ENV', 'development')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'divya126')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form["url"]
        try:
            ydl_opts = {
    'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
    'merge_output_format': 'mp4'
}


            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                filename = ydl.prepare_filename(info)
                file = os.path.basename(filename)
                return render_template("index.html", download_url=f"/download/{file}")
        except Exception as e:
            return f"❌ Error downloading: {str(e)}"
    return render_template("index.html", download_url=None)

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
