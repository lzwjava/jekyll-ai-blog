import shutil
import subprocess


def update_marp_pdf(marp_md, public_pdf=None):
    md_path = Path(marp_md)
    if not md_path.exists():
        print(f"❌ File not found: {marp_md}")
        return

    base_dir = md_path.parent
    stem = md_path.stem

    pdf_path = base_dir / f"{stem}.pdf"
    if public_pdf:
        public_path = Path(public_pdf)
    else:
        public_path = base_dir / f"{stem}_public.pdf"

    result = subprocess.run(
        ["marp", "--pdf", "--allow-local-files", str(md_path)],
        cwd=base_dir,
    )
    if result.returncode != 0:
        print(f"❌ Marp failed for {marp_md}")
        return

    if public_path.exists():
        public_path.unlink()
    shutil.copy(pdf_path, public_path)
    print(f"✅ Updated {public_path}")


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "marp_md", nargs="?", default="assets/marp/neural_networks_to_agents.md"
    )
    parser.add_argument(
        "--public", default="assets/marp/neural_networks_to_agents_public.pdf"
    )
    args = parser.parse_args()

    update_marp_pdf(args.marp_md, args.public)
