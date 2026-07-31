from email.mime.text import MIMEText


class EmailTemplate:
    @staticmethod
    def verification_code_template(email: str, code: str) -> MIMEText:
        code_html = "".join(
            f"""
            <span style="
                display:inline-block;
                width: 44px;
                height: 48px;
                line-height: 48px;
                margin: 0 4px;
                text-align: center;
                font-size: 24px;
                font-weight: bold;
                color: #2f0ea8;
                background: #f8f8ff;
                border-radius: 8px;
                border: 1px solid #cbd5e0;
                font-family: 'Courier New', monospace;
            ">{digit}</span>
            """
            for digit in code
        )

        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f6f8; padding: 30px;">
                <div style="
                    max-width: 480px;
                    margin: auto;
                    background: #ffffff;
                    padding: 30px;
                    border-radius: 12px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                ">
                    <h2 style="color: #1a202c; text-align: center; margin-bottom: 20px;">
                        Your Verification Code
                    </h2>

                    <p style="color: #4a5568; font-size: 15px;">
                        Hello <b>{email}</b>,
                    </p>

                    <p style="color: #4a5568; font-size: 15px;">
                        Use the following verification code to continue:
                    </p>

                    <div style="text-align: center; margin: 25px 0;">
                        {code_html}
                    </div>

                    <p style="color: #718096; font-size: 14px; text-align: center;">
                        This code is valid for <b>2 minutes</b>.
                    </p>

                    <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 30px 0;">

                    <p style="color: #a0aec0; font-size: 12px; text-align: center;">
                        If you didn’t request this code, you can safely ignore this email.
                    </p>
                </div>
            </body>
        </html>
        """

        msg = MIMEText(html, "html")
        msg["Subject"] = "Your Verification Code"
        return msg
