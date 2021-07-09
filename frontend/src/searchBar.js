import "./searchBar.css";
import SearchContent from "./searchContent";
import React, { useState } from "react";

const SearchBar = () => {
  const [content, setContent] = useState("");
  const [buttonPressed, setButtonPressed] = useState(false);

  const validateForm = () => {
    return content.length > 0;
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    setButtonPressed(true);
  };

  return (
    <div class="search">
      <form class="form" onSubmit={handleSubmit} style={{ margin: "10px" }}>
        <lable style={{ fontSize: "18px", marginRight: "10px" }}>
          Search:{" "}
        </lable>
        <input
          class="search-input"
          type="text"
          value={content}
          onChange={(e) => {
            setContent(e.target.value);
            if (buttonPressed) {
              setButtonPressed(false);
            }
          }}
          style={{ width: "300px", height: "28px", marginRight: "10px" }}
        />
        <button type="submit" disabled={!validateForm()}>
          Enter
        </button>
      </form>
      <div class="input-format">
        Input Format: [professor name], [institution name]
      </div>
      {buttonPressed ? <SearchContent content={content} /> : <div></div>}
    </div>
  );
};

export default SearchBar;
