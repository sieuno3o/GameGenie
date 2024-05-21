import defaultDashboard from "@/layout/dashboard/DefaultDashboard";

const CommunityMainPage = () => import("@/views/community/CommunityMainPage.vue");

const communityRoutes = [
  {
    path: "",
    component: defaultDashboard,
    children: [
      {
        path: "",
        name: "communityMain",
        component: CommunityMainPage,
      },
    ],
  }, 
];

export default communityRoutes;
