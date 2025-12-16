export default function CitySelect({ city, setCity, cities }) {
  return (
    <div className="inline-flex items-center gap-2
                    bg-white/90 backdrop-blur
                    border border-gray-200
                    rounded-full px-4 py-2
                    shadow-sm">
      <span className="text-sm text-gray-500">📍</span>
      <select
        value={city}
        onChange={(e) => setCity(e.target.value)}
        className="bg-transparent text-sm font-semibold
                   outline-none cursor-pointer"
      >
        {cities.map((c) => (
          <option key={c} value={c}>
            {c.toUpperCase()}
          </option>
        ))}
      </select>
    </div>
  );
}
