import React, { useState, useEffect } from "react";

const ProfessorPage = (props) => {
  const { content } = props;
  const [loading1, setLoading1] = useState(true);
  const [loading2, setLoading2] = useState(true);

  const [name, setName] = useState("");
  const [bio, setBio] = useState("");
  const [award, setAward] = useState("");
  const [education, setEducation] = useState("");
  const [institution, setInstitution] = useState("");
  const [researchInterest, setResearchInterest] = useState("");
  const [publications, setPublications] = useState([]);

  const splits = content.split(", ");
  const format = splits.length === 2;
  const professorName = splits[0];
  const institutionName = splits[1];

  useEffect(() => {
    const backend_prefix = "http://127.0.0.1:5000/";
    const professor_prefix = "page?";
    const publication_prefix = "publication?";
    const professor_url =
      backend_prefix +
      professor_prefix +
      "professor=" +
      professorName +
      "&institution=" +
      institutionName;
    const publication_url =
      backend_prefix +
      publication_prefix +
      "professor=" +
      professorName +
      "&institution=" +
      institutionName;

    const fetch_data = () => {
      fetch(professor_url, {
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
          setName(data[0]);
          setBio(data[1]);
          setAward(data[2]);
          setEducation(data[3]);
          setInstitution(data[4]);
          setResearchInterest(data[5]);
          setLoading1(false);
        });
      fetch(publication_url, {
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
          setPublications(data);
          setLoading2(false);
        });
    };

    fetch_data();
  }, [professorName, institutionName]);

  return (
    <div>
      {format ? (
        <div
          style={{
            textAlign: "left",
            paddingLeft: "10%",
          }}
        >
          {loading1 || loading2 ? (
            <div
              style={{
                fontSize: "26px",
                fontWeight: "bold",
              }}
            >
              loading...
            </div>
          ) : (
            <div
              style={{
                fontSize: "22px",
              }}
            >
              <div
                style={{
                  fontSize: "32px",
                  fontWeight: "bold",
                  marginBottom: "20px",
                }}
              >
                {name}
              </div>
              <div
                style={{
                  display: "flex",
                  fontWeight: "bold",
                }}
              >
                <div>Bio: </div>
                <div
                  style={{
                    fontWeight: "normal",
                    paddingLeft: "220px",
                    marginBottom: "10px",
                  }}
                >
                  {bio}
                </div>
              </div>

              <div style={{ display: "flex", fontWeight: "bold" }}>
                <div>Award: </div>
                <div
                  style={{
                    fontWeight: "normal",
                    paddingLeft: "186px",
                    marginBottom: "10px",
                  }}
                >
                  {award}
                </div>
              </div>

              <div style={{ display: "flex", fontWeight: "bold" }}>
                <div>Education: </div>
                <div
                  style={{
                    fontWeight: "normal",
                    paddingLeft: "150px",
                    marginBottom: "10px",
                  }}
                >
                  {education}
                </div>
              </div>

              <div style={{ display: "flex", fontWeight: "bold" }}>
                <div>Institution: </div>
                <div
                  style={{
                    fontWeight: "normal",
                    paddingLeft: "145px",
                    marginBottom: "10px",
                  }}
                >
                  {institution}
                </div>
              </div>

              <div style={{ display: "flex", fontWeight: "bold" }}>
                <div>Research Interest: </div>
                <div
                  style={{
                    fontWeight: "normal",
                    paddingLeft: "76px",
                    marginBottom: "10px",
                  }}
                >
                  {researchInterest}
                </div>
              </div>

              <div style={{ display: "flex", fontWeight: "bold" }}>
                <div>Publications: </div>
                <div
                  style={{
                    fontWeight: "normal",
                    paddingLeft: "126px",
                    marginBottom: "10px",
                  }}
                >
                  <div>
                    {publications.map((paper, index) => (
                      <p>
                        <a href={paper[1]} style={{ marginBottom: "6px" }}>
                          {paper[0]}
                        </a>
                      </p>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      ) : (
        <div>Check Input Format Above</div>
      )}
    </div>
  );
};
export default ProfessorPage;
