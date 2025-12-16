const API_URL = "http://localhost:8000/api/recommend";

export async function getRecommendation(city, query) {
  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ city, query }),
  });

  return res.json();
}
