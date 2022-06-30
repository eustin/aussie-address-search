import { useState } from "react";
import Logo from "./components/Logo";
import Search from "./components/Search";

function App() {
  const [searchText, setSearchText] = useState("");
  const [selectedAddress, setSelectedAddress] = useState("");

  const searchProps = { setSelectedAddress, searchText, setSearchText };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gradient-to-tr from-yellow-200 via-green-200 to-green-500 overflow-hidden">
      <Logo width="280" />
      <div className="text-4xl mb-5 mt-10 font-bold text-slate-700">
        Welcome to Aussie Address Search!
      </div>
      <Search {...searchProps} />
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
