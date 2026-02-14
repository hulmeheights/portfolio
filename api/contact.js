export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const API_KEY = 're_URPqETB7_JE2chzFcbSVHXFngdzZPnE4h';
  const { name, email, message, type } = req.body;

  if (type === 'contact') {
    const response = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: 'Haydon <haydon@hulmeheights.xyz>',
        to: 'hulmeheights@gmail.com',
        subject: `New message from ${name}`,
        html: `<p><strong>Name:</strong> ${name}</p><p><strong>Email:</strong> ${email}</p><p><strong>Message:</strong> ${message}</p>`,
      }),
    });

    if (response.ok) {
      return res.status(200).json({ success: true });
    } else {
      return res.status(500).json({ error: 'Failed to send' });
    }
  }

  if (type === 'subscribe') {
    // Get the default audience ID first
    const audiencesRes = await fetch('https://api.resend.com/audiences', {
      headers: { 'Authorization': `Bearer ${API_KEY}` },
    });
    const audiencesData = await audiencesRes.json();
    const audienceId = audiencesData.data[0].id;

    // Add contact to audience
    await fetch(`https://api.resend.com/audiences/${audienceId}/contacts`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email,
        unsubscribed: false,
      }),
    });

    // Also notify you
    const response = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: 'Haydon <haydon@hulmeheights.xyz>',
        to: 'hulmeheights@gmail.com',
        subject: `New subscriber: ${email}`,
        html: `<p>New email signup: <strong>${email}</strong></p><p>They've been automatically added to your Resend audience.</p>`,
      }),
    });

    if (response.ok) {
      return res.status(200).json({ success: true });
    } else {
      return res.status(500).json({ error: 'Failed to send' });
    }
  }
}
