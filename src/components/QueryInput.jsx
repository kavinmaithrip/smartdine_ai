export default function QueryInput({ query, setQuery }) {
  return (
    <input
      placeholder="Feeling tired? Craving something spicy?"
      value={query}
      onChange={e => setQuery(e.target.value)}
    />
  );
}
