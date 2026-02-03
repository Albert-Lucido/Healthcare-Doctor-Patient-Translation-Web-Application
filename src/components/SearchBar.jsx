import { useState } from 'react';
import './SearchBar.css';

function SearchBar({ onSearch, onClear }) {
  const [query, setQuery] = useState('');

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query);
    }
  };

  const handleClear = () => {
    setQuery('');
    onClear();
  };

  return (
    <div className="search-bar">
      <form className="search-form" onSubmit={handleSearch}>
        <input
          type="text"
          className="search-input"
          placeholder="Search conversation history..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          type="submit"
          className="btn btn-primary btn-sm"
          disabled={!query.trim()}
        >
          🔍 Search
        </button>
        {query && (
          <button
            type="button"
            className="btn btn-secondary btn-sm"
            onClick={handleClear}
          >
            ✕ Clear
          </button>
        )}
      </form>
    </div>
  );
}

export default SearchBar;
