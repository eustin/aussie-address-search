function App() {
  return (
    <div>
      <div>Welcome to Aussie Address Search!</div>
      <label htmlFor="searchBox">
        Search for your address in the G-NAF database here:
      </label>
      <input id="searchBox" placeholder="e.g. 123 Fake Street" />
      <input type="submit" value="Search"/>
    </div>
  );
}

export default App;
