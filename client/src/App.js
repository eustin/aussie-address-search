import { useState } from "react";

function App() {
  const [searchText, setSearchText] = useState("");

  const onChangeHandler = (event) => {
    const text = event.target.value;
    setSearchText(text);
  }

  return (
    <div>
      <div>Welcome to Aussie Address Search!</div>

      <label htmlFor="searchBox">
        Search for your validated address, here:
      </label>
      <input
        id="searchBox"
        type="text"
        placeholder="123 Fake Street"
        onChange={onChangeHandler}
      />
    </div>
  );
}

export default App;
