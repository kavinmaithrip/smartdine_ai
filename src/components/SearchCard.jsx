export default function SearchCard({
  query,
  setQuery,
  onSearch,
  onSurprise,
  citySelect,
}) {
  return (
    <div className="relative -mt-20">
      <div className="bg-white rounded-2xl shadow-xl p-6 max-w-3xl mx-auto space-y-4">
        <h2 className="text-xl font-semibold text-gray-800">
          What are you craving today?
        </h2>

        {citySelect}

        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Eg: cheesy but affordable, comfort food, something sweet…"
          className="w-full p-4 border rounded-xl focus:ring-2 focus:ring-red-400 outline-none"
        />

        <div className="flex gap-4">
          <button
            onClick={onSearch}
            className="flex-1 bg-red-500 text-white py-3 rounded-xl font-semibold
                       hover:bg-red-600 active:scale-95 transition"
          >
            Recommend
          </button>

          <button
            onClick={onSurprise}
            className="flex-1 bg-gray-900 text-white py-3 rounded-xl font-semibold
                       hover:bg-black active:scale-95 transition"
          >
            Surprise Me 🎲
          </button>
        </div>
      </div>
    </div>
  );
}
