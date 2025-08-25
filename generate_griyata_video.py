#!/usr/bin/env python3
import argparse
import os
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import (
    AudioClip,
    ColorClip,
    CompositeVideoClip,
    ImageClip,
)

W, H = 1920, 1080
FPS = 24
DURATION = 12.0  # detik

BG_COLOR = (10, 34, 57)      # navy-ish
ACCENT = (255, 185, 0)       # aksen
TEXT_COLOR = (240, 250, 248) # near-white


def find_logo_path(cli_logo: str | None) -> str:
    if cli_logo and Path(cli_logo).is_file():
        return cli_logo
    candidates = [
        "assets/logo-griyata.png",
        "assets/logo.png",
    ]
    for p in candidates:
        if Path(p).is_file():
            return p
    raise FileNotFoundError(
        "Logo tidak ditemukan. Pastikan ada di assets/logo-griyata.png."
    )


def load_font(size: int):
    # Coba font umum di runner Ubuntu
    common_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for p in common_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size=size)
            except Exception:
                pass
    return ImageFont.load_default()


def make_text_image(text: str, size: int, color=TEXT_COLOR, padding=20) -> Image.Image:
    font = load_font(size)
    dummy = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
    draw = ImageDraw.Draw(dummy)
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0] + padding * 2
    h = bbox[3] - bbox[1] + padding * 2
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((padding, padding), text, font=font, fill=color)
    return img


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--logo", type=str, default=None, help="Path logo PNG")
    parser.add_argument("--out", type=str, default="outputs/griyata_promo.mp4", help="Output MP4")
    parser.add_argument("--title", type=str, default="Griyata", help="Judul")
    parser.add_argument("--subtitle1", type=str, default="Solusi KPR digital", help="Subjudul 1")
    parser.add_argument("--subtitle2", type=str, default="Cepat • Mudah • Transparan", help="Subjudul 2")
    args = parser.parse_args()

    logo_path = find_logo_path(args.logo)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Background
    bg = ColorClip(size=(W, H), color=BG_COLOR).set_duration(DURATION)

    # Dekorasi bar aksen
    bar_h = 16
    bar = ColorClip(size=(int(W * 0.6), bar_h), color=ACCENT).set_duration(DURATION)
    bar = bar.set_position(lambda t: ("center", H * 0.72 + 20 * np.sin(2 * np.pi * (t / DURATION))))

    # Logo
    logo = ImageClip(logo_path).set_duration(DURATION)
    target_w = int(W * 0.5)
    if logo.w > target_w:
        logo = logo.resize(width=target_w)

    # Animasi logo
    logo = (
        logo
        .resize(lambda t: 0.85 + 0.15 * min(1, t / 1.6))
        .set_position(lambda t: ("center", H * 0.36 - 15 * np.cos(2 * np.pi * (t / 6.0))))
        .fadein(0.8)
        .fadeout(0.6)
    )

    # Teks
    title_img = make_text_image(args.title, size=80, color=TEXT_COLOR)
    subtitle1_img = make_text_image(args.subtitle1, size=48, color=(210, 230, 228))
    subtitle2_img = make_text_image(args.subtitle2, size=40, color=(185, 205, 202))

    title_clip = (
        ImageClip(np.array(title_img))
        .set_duration(DURATION - 1)
        .set_start(0.8)
        .set_position(("center", H * 0.62))
        .fadein(0.6)
        .fadeout(0.6)
    )

    subtitle1_clip = (
        ImageClip(np.array(subtitle1_img))
        .set_duration(DURATION - 2)
        .set_start(1.4)
        .set_position(("center", H * 0.68))
        .fadein(0.6)
        .fadeout(0.6)
    )

    subtitle2_clip = (
        ImageClip(np.array(subtitle2_img))
        .set_duration(DURATION - 3)
        .set_start(2.0)
        .set_position(("center", H * 0.74))
        .fadein(0.6)
        .fadeout(0.6)
    )

    comp = CompositeVideoClip([bg, bar, logo, title_clip, subtitle1_clip, subtitle2_clip], size=(W, H))

    # Audio hening agar kompatibel
    silent_audio = AudioClip(lambda t: 0 * t, duration=DURATION, fps=44100)
    comp = comp.set_audio(silent_audio)

    # Tulis video
    comp.write_videofile(
        str(out_path),
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        audio_bitrate="192k",
        preset="medium",
        bitrate="3000k",
        threads=2,
        ffmpeg_params=["-movflags", "+faststart", "-pix_fmt", "yuv420p"],
        verbose=False,
        logger=None,
    )


if __name__ == "__main__":
    main()