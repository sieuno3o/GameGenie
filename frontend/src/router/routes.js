import defaultRoutes from "./routes/defaultRoutes";
import communityRoutes from "./routes/communityRoutes";
import accountRoutes from "./routes/accountRoutes";
import recommendationsRoutes from "./routes/recommendsRoutes";

import defaultLayout from "../layout/TheLayout";
import accountLayout from "../layout/TheAccountLayout";

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
    path: "/",
    component: accountLayout,
    children: accountRoutes,
  },
  {
    path: "/recommendations",
    component: defaultLayout,
    children: recommendationsRoutes,
  },
];

export default routes;
