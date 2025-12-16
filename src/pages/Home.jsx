import { useState, useEffect } from "react";
import Header from "../components/Header";
import SearchBar from "../components/SearchBar";
import RecommendationCard from "../components/RecommendationCard";
import CitySelect from "../components/CitySelect";
import { getRecommendation } from "../services/api";

export default function Home() {
  const [city, setCity] = useState("");
  const [cities, setCities] = useState([]);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [hasSearched, setHasSearched] = useState(false);
  const [weather, setWeather] = useState(null);

  
  useEffect(() => {
    fetch("http://localhost:8000/cities")
      .then((res) => res.json())
      .then((data) => {
        setCities(data.cities || []);
        setCity(data.cities?.[0] || "");
      })
      .catch(() => {
        setError("Unable to load cities.");
      });
  }, []);

  async function handleRecommend(surprise) {
    if (loading) return;

    setLoading(true);
    setError("");
    setResults([]);
    setHasSearched(true);

    try {
      const data = await getRecommendation({ query, city, surprise });
      setResults(data.results || []);
      setWeather(data.weather || null);
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="bg-gradient-to-br from-orange-50 via-red-50 to-pink-50 min-h-screen">

      
      <Header />

      
      <section className="relative">
        <div className="h-56 bg-gradient-to-r from-red-500 to-orange-400"></div>

        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center px-6">
            <h1 className="text-5xl font-extrabold text-white mb-4 leading-tight">
              Discover food that
              <span className="block text-yellow-200">
                matches your mood
              </span>
            </h1>
            <p className="text-white/90 text-lg max-w-2xl mx-auto">
              Tell SmartDine how you feel — tired, happy, stressed or confused.
              We’ll recommend food that feels just right.
            </p>
          </div>
        </div>
      </section>

      
      <div className="max-w-5xl mx-auto px-6 mt-10">
        <h2 className="text-3xl font-extrabold text-gray-900 mb-4">
          What are you craving today?
        </h2>

        <CitySelect
          city={city}
          setCity={setCity}
          cities={cities}
        />

        <SearchBar
          query={query}
          setQuery={setQuery}
          onSearch={() => handleRecommend(false)}
          onSurprise={() => handleRecommend(true)}
          disabled={loading}
        />
      </div>

      
      <section className="max-w-5xl mx-auto px-6 mt-14 pb-20">

        {loading && (
          <div className="text-center text-gray-600 text-lg animate-pulse">
            Finding the perfect dish for you…
          </div>
        )}

        {!loading && error && (
          <div className="text-center text-red-500 mt-8 font-medium">
            {error}
          </div>
        )}

        {!loading && hasSearched && results.length === 0 && !error && (
          <div className="text-center text-gray-500 mt-10">
            No matching recommendations found. Try rephrasing your craving.
          </div>
        )}

        {!hasSearched && !loading && (
          <div className="text-center text-gray-400 mt-10">
            Start by telling SmartDine what you’re craving.
          </div>
        )}

        {weather && results.length > 0 && (
          <div className="text-center text-sm text-gray-500 mt-4">
            Based on current {weather.category} weather in {city}
          </div>
        )}

        <div className="grid gap-6 mt-6">
          {results.map((r, i) => (
            <RecommendationCard key={i} data={r} />
          ))}
        </div>
      </section>
    </div>
  );
}
