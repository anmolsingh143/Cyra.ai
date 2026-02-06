export async function sendToBackend(
  text: string,
  emailId: string | null,
  to?: string | null,
  subject?: string | null,
  body?: string | null
) {
  const res = await fetch("http://127.0.0.1:9000/voice", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      text,
      email_id: emailId,
      to,
      subject,
      body,
    }),
  });

  if (!res.ok) throw new Error("Backend error");
  return res.json();
}
