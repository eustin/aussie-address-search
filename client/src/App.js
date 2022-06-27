import { useState } from "react";
import Logo from "./components/Logo";

function App() {
  const [searchText, setSearchText] = useState("");

  const onChangeHandler = (event) => {
    const text = event.target.value;
    setSearchText(text);
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gradient-to-tr from-yellow-200 via-green-200 to-green-500">
      <Logo height="280" />
      <div className="text-4xl mb-5 mt-10 font-bold text-slate-700">
        Welcome to Aussie Address Search!
      </div>
      <label htmlFor="searchBox" className="text-xl mb-5 text-slate-700">
        Search for your validated address, here:
      </label>
      <input
        id="searchBox"
        className="border-2 p-2 border-gray-400 rounded w-1/2"
        type="text"
        placeholder="e.g. 123 Fake Street"
        onChange={onChangeHandler}
      />
    </div>
  );
}

export default App;
