import { useHistory } from "react-router-dom";
const SecondPage = () => {
  let history = useHistory();
  return (
    <div>
      {" "}
      <button onClick={() => history.push("/third")}>
        Go to HomePage
      </button>{" "}
    </div>
  );
};
