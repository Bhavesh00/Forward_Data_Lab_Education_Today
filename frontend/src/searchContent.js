import React, { useState, useEffect } from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useRouteMatch,
  useParams,
} from "react-router-dom";
import ProfessorPage from "./professorPage";

const SearchContent = (props) => {
  const { content } = props;
  const [loading, setLoading] = useState(true);
  const [rankList, setRankList] = useState([]);

  const splits = content.split(", ");
  const format = splits.length === 2;
  const professorName = splits[0];
  const institutionName = splits[1];

  useEffect(() => {
    const backend_prefix = "http://127.0.0.1:5000/search?";
    const url =
      backend_prefix +
      "professor=" +
      professorName +
      "&institution=" +
      institutionName;

    fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
      })
      .then((data) => {
        setRankList(data);
        console.log(data);
        setLoading(false);
      });
  }, [professorName, institutionName]);

  return (
    <div>
      {loading ? (
        <div>loading...</div>
      ) : (
        <div>
          {rankList.map((professor, index) => (
            <div
              style={{
                textAlign: "left",
                paddingLeft: "35%",
              }}
            >
              <Link to={`/professor/${professor[0]}_&_${professor[1]}`}>
                <div
                  style={{
                    fontSize: 18,
                    marginTop: "8px",
                  }}
                >
                  {index + 1}: {professor[0]}
                </div>
              </Link>
              <div
                style={{
                  fontSize: 14,
                  paddingLeft: "15px",
                }}
              >
                institution: {professor[1]}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SearchContent;
