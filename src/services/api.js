const API_BASE = "http://localhost:8000";

export async function getRecommendation({ query, city, surprise }) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 20000); // 20s timeout

  try {
    const res = await fetch(`${API_BASE}/recommend`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      signal: controller.signal,
      body: JSON.stringify({
        query: query || "",
        city: city.toLowerCase(),
        surprise: Boolean(surprise),
      }),
    });

    clearTimeout(timeout);

    if (!res.ok) {
      let errorMessage = "Recommendation failed";
      try {
        const err = await res.json();
        errorMessage = err.message || err.error || errorMessage;
      } catch {
        errorMessage = await res.text();
      }
      throw new Error(errorMessage);
    }

    return await res.json();

  } catch (err) {
    if (err.name === "AbortError") {
      throw new Error("Request timed out. Please try again.");
    }
    throw err;
  }
}
