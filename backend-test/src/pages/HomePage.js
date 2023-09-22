import { useHistory } from "react-router-dom";

const FirstPage = () => {
    let history = useHistory();

    return (
        <div>
            <button onClick={() => history.push("/second")}>Go to Second Page</button>
        </div>
    );
};