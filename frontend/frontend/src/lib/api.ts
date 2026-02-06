export async function sendToBackend(
  text: string,
  emailId: string | null,
  to?: string | null,
  subject?: string | null,
  body?: string | null
) {
  const res = await fetch("https://cyra-ai.onrender.com", {
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
