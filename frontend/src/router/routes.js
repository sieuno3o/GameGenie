import defaultRoutes from "./routes/defaultRoutes";
import communityRoutes from "./routes/communityRoutes";
import accountRoutes from "./routes/accountRoutes";

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
  },
  {
    path: "/account",
    component: defaultLayout,
    children: accountRoutes,
  }
];

export default routes;