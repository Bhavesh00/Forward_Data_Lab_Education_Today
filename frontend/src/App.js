import "./App.css";
import SearchBar from "./searchBar";
import ProfessorPage from "./professorPage";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useParams,
} from "react-router-dom";

function App() {
  return (
    <Router>
      <div className="App">
        <Link to="/">
          <h1>Education Today</h1>
        </Link>

        <Switch>
          <Route path="/professor/:professor" component={Professor}></Route>
          <Route path="/">
            <SearchBar />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

function Professor(props) {
  const { professor } = useParams();
  const splits = professor.split("_&_");
  return <ProfessorPage content={splits[0] + ", " + splits[1]} />;
}

export default App;
// Jiawei Han, University of Illinois at Urbana-Champaign
