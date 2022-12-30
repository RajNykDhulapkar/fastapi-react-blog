import { useLocation } from "react-router";

import styles from "./error.module.css";

export default function Homepage() {
    const location = useLocation();
    console.log(location);
    return (
        <div className={styles.main}>
            <div className={styles.fof}>
                <h1>Error 404</h1>
            </div>
        </div>
    );
}
