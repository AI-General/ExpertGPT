import { useHistory } from "react-router-dom";
const SecondPage = () => {
  let history = useHistory();
  return (
    <div>
      {" "}
      <button onClick={() => history.push("/")}>
        Go to Third Page
      </button>{" "}
    </div>
  );
};
