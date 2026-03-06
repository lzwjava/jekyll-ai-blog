import json
import subprocess
import tempfile
import os
import base64


def lambda_handler(event, context):
    try:
        # Get LaTeX content from event
        latex_content = event.get("latex_content", "")
        if not latex_content:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No LaTeX content provided"}),
            }

        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            tex_file = os.path.join(temp_dir, "document.tex")
            pdf_file = os.path.join(temp_dir, "document.pdf")

            # Write LaTeX content to file
            with open(tex_file, "w") as f:
                f.write(latex_content)

            # Compile LaTeX to PDF
            result = subprocess.run(
                [
                    "pdflatex",
                    "-output-directory",
                    temp_dir,
                    "-interaction=nonstopmode",
                    tex_file,
                ],
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                return {
                    "statusCode": 500,
                    "body": json.dumps(
                        {"error": "LaTeX compilation failed", "details": result.stderr}
                    ),
                }

            # Read PDF file and encode as base64
            with open(pdf_file, "rb") as f:
                pdf_data = base64.b64encode(f.read()).decode("utf-8")

            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/pdf"},
                "body": pdf_data,
                "isBase64Encoded": True,
            }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
