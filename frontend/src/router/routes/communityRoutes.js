import defaultDashboard from "@/layout/dashboard/DefaultDashboard";

const CommunityMainPage = () => import("@/views/community/CommunityMainPage.vue");
const CommunityDetailPage = () => import("@/views/community/CommunityMainPage.vue");
const CommunityCreatePage = () => import("@/views/community/CommunityCreatePage.vue");

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
      {
        path: "detail",
        name: "communityDetail",
        component: CommunityDetailPage,
      },
      {
        path: "create",
        name: "communityCreate",
        component: CommunityCreatePage,
      },
    ],
  }, 
];  

export default communityRoutes;
