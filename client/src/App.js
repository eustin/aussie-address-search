import { useState } from "react";
import Logo from "./components/Logo";

const INITIAL_SUGGESTIONS = [
  { id: "1", suggestion: "182 Hello Street, Sydney" },
  { id: "2", suggestion: "123 Fake Street" },
  { id: "3", suggestion: "Broadway" },
];

const INITIAL_SEARCH_TEXT = "123 Fake";

function App() {
  const [searchText, setSearchText] = useState(INITIAL_SEARCH_TEXT);
  const [suggestions, setSuggestions] = useState(INITIAL_SUGGESTIONS);

  const selectedAddress = "123 Fake Street";

  // const onChangeHandler = (event) => {
  //   const text = event.target.value;
  //   setSearchText(text);
  // };

  const suggestionsStyles =
    "absolute z-10 top-full left-0 right-0 rounded border-2 border-gray-400";

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
          // onChange={onChangeHandler}
        />
        <div
          className={
            suggestions.length === 0
              ? suggestionsStyles.concat(" hidden")
              : suggestionsStyles
          }
        >
          {Boolean(suggestions) &&
            suggestions.map(({ id, suggestion }) => (
              <div className="p-1 bg-white hover:bg-gray-200" key={id}>
                {suggestion}
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
