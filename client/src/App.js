import { useState } from "react";
import Logo from "./components/Logo";

const INITIAL_SUGGESTIONS = [
  { id: "1", suggestion: "182 Hello Street, Sydney" },
  { id: "2", suggestion: "123 Fake Street" },
  { id: "3", suggestion: "Broadway" },
];

function App() {
  const [searchText, setSearchText] = useState("");
  const [suggestions, setSuggestions] = useState(INITIAL_SUGGESTIONS);
  const [selectedAddress, setSelectedAddress] = useState("");
  const [suggestionsVisible, setSuggestionsVisible] = useState(false);

  const onChangeHandler = (event) => {
    const text = event.target.value;
    setSearchText(text);
    setSuggestionsVisible(true);
  };

  const onClickHandler = (event) => {
    setSelectedAddress(event.target.innerText);
    setSuggestionsVisible(false);
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gradient-to-tr from-yellow-200 via-green-200 to-green-500 overflow-hidden">
      <Logo height="280" />
      <div className="text-4xl mb-5 mt-10 font-bold text-slate-700">
        Welcome to Aussie Address Search!
      </div>
      <label htmlFor="searchBox" className="text-xl mb-5 text-slate-700">
        Search for your validated address, here:
      </label>
      <div id="searchContainer" className="relative inline-block w-1/3 ">
        <input
          id="searchBox"
          className="p-2 border-2 border-gray-400 rounded w-full"
          type="text"
          placeholder="e.g. 123 Fake Street"
          value={searchText}
          onChange={onChangeHandler}
        />
        <div
          className={`absolute z-10 top-full left-0 right-0 rounded border-2 border-gray-400 ${
            suggestions.length === 0 || !suggestionsVisible ? "hidden" : ""
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
      <div className="mt-5 text-xl">
        {Boolean(selectedAddress) ? (
          <div>Your validated address is {selectedAddress}!</div>
        ) : null}
      </div>
      <a
        className="mt-5 text-xs"
        href="https://www.vecteezy.com/free-vector/nature"
      >
        Wombat logo from Nature Vectors by Vecteezy. Thank you!
      </a>
    </div>
  );
}

export default App;
