import defaultRoutes from "./routes/defaultRoutes";
import communityRoutes from "./routes/communityRoutes";

import defaultLayout from "../layout/TheLayout";

const routes = [
  {
    path: "/",
    component: defaultLayout,
    children: defaultRoutes,
  },
  {
    path: "/community",
    component: defaultLayout,
    children: communityRoutes,
  }
];

export default routes;