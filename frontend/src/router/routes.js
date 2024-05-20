import defaultRoutes from "./routes/defaultRoutes";
import defaultLayout from "../layout/TheLayout";

const routes = [
  {
    path: "/",
    component: defaultLayout,
    children: defaultRoutes,
  },
];

export default routes;