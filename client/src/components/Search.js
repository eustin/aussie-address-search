import { useState } from "react";
import { httpPostSearch } from "../api/addressSearch";

const Search = ({ setSelectedAddress, searchText, setSearchText }) => {
  const [suggestions, setSuggestions] = useState([]);
  const [suggestionsVisible, setSuggestionsVisible] = useState(false);

  const onChangeHandler = (event) => {
    const text = event.target.value;
    setSearchText(text);
    setSuggestionsVisible(true);

    const getSuggestions = async () => {
      if (text.length > 0) {
        const { suggestions } = await httpPostSearch(text);
        setSuggestions(suggestions);
      } else {
        setSuggestions("");
      }
    };

    getSuggestions();
  };

  const onClickHandler = (event) => {
    const selectedAddress = event.target.innerText;
    setSelectedAddress(selectedAddress);
    setSuggestionsVisible(false);
    setSearchText(selectedAddress);
  };

  const onFocusHandler = () => {
    if (suggestions) {
      setSuggestionsVisible(true);
    }
  };

  return (
    <div className="flex flex-col">
      <label htmlFor="searchBox" className="text-xl mb-5 text-slate-700">
        Search for your validated address, here:
      </label>
      <div id="searchContainer" className="relative inline-block w-full ">
        <input
          id="searchBox"
          className="p-2 border-2 border-gray-400 rounded w-full"
          type="text"
          placeholder="e.g. 123 Fake Street"
          autoComplete="off"
          value={searchText}
          onChange={onChangeHandler}
          onFocus={onFocusHandler}
        />
        <div
          className={`absolute z-10 top-full left-0 right-0 rounded border-2 border-gray-400 ${
            suggestions.length === 0 ||
            !suggestionsVisible ||
            searchText.length === 0
              ? "hidden"
              : ""
          }`}
        >
          {Boolean(suggestions) &&
            suggestions.map(({ id, suggestion }) => (
              <div className="p-1 bg-white hover:bg-gray-200" key={id}>
                <button className="w-full text-left" onClick={onClickHandler}>
                  {suggestion}
                </button>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
};

export default Search;
