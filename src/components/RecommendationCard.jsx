export default function RecommendationCard({ data }) {
  const rating =
    typeof data.Average_Rating === "number"
      ? Math.max(0, Math.min(data.Average_Rating, 5))
      : null;

  const ratingColor =
    rating >= 4.5
      ? "bg-green-700"
      : rating >= 4.0
      ? "bg-green-600"
      : rating >= 3.5
      ? "bg-yellow-500"
      : "bg-red-500";

  return (
    <div className="bg-white rounded-2xl shadow-md hover:shadow-xl transition p-5">

      {/* HEADER */}
      <div className="flex justify-between items-start gap-4">
        <div>
          <h3 className="text-lg font-bold text-gray-800">
            {data.Item_Name}
          </h3>
          <p className="text-sm text-gray-500">
            {data.Restaurant_Name}
          </p>
        </div>

        {/* RATING BADGE */}
        {rating !== null ? (
          <span
            className={`inline-flex items-center gap-1
                        ${ratingColor} text-white
                        text-xs px-3 py-1 rounded-full font-semibold`}
          >
            ⭐ {rating.toFixed(1)}
          </span>
        ) : (
          <span
            className="inline-flex items-center gap-1
                       bg-gray-200 text-gray-700
                       text-xs px-3 py-1 rounded-full font-semibold"
          >
            ⭐ Popular pick
          </span>
        )}
      </div>

      {/* EXPLANATION */}
      <p className="mt-3 text-sm text-gray-700 italic leading-relaxed">
        {data.explanation}
      </p>

      {/* TAGS */}
      <div className="mt-4 flex flex-wrap gap-2">
        {data.Is_Bestseller === 1 && (
          <span className="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">
            Bestseller
          </span>
        )}

        {data.Is_Expensive === 0 && (
          <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
            Budget-friendly
          </span>
        )}
      </div>
    </div>
  );
}
