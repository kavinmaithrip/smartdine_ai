export default function SearchBar({
  query,
  setQuery,
  onSearch,
  onSurprise,
}) {
  return (
    <div className="w-full max-w-3xl mx-auto mt-8">

      {/* Query Bar */}
      <div className="flex items-center bg-white
                      rounded-full shadow-lg
                      px-6 py-4
                      focus-within:ring-2
                      focus-within:ring-red-400
                      transition">

        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="I feel like something cheesy, comforting, or sweet…"
          className="flex-1 bg-transparent
                     outline-none text-base"
        />

        <button
          onClick={onSearch}
          className="ml-4 text-red-500 font-semibold
                     hover:text-red-600 transition"
        >
          🔍
        </button>
      </div>

      {/* Actions */}
      <div className="flex justify-center gap-6 mt-6">
        <button
          onClick={onSearch}
          className="px-8 py-3 rounded-full
                     bg-red-500 text-white font-semibold
                     hover:bg-red-600 active:scale-95 transition"
        >
          Recommend
        </button>

        <button
          onClick={onSurprise}
          className="px-8 py-3 rounded-full
                     bg-gray-900 text-white font-semibold
                     hover:bg-black active:scale-95 transition"
        >
          Surprise Me 🎲
        </button>
      </div>
    </div>
  );
}
