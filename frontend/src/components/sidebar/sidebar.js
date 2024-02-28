import {
    Card,
    List,
    ListItem,
    ListItemPrefix,
} from "@material-tailwind/react";
import {
    PresentationChartBarIcon,
    UserCircleIcon,
    Cog6ToothIcon,
} from "@heroicons/react/24/solid";

export function DefaultSidebar() {
    return (
        <Card className="h-[calc(100vh-2rem)] w-full max-w-[20rem] p-4 shadow-xl shadow-blue-gray-900/5">
            <List>
                <ListItem>
                    <ListItemPrefix>
                        <PresentationChartBarIcon className="h-5 w-5"/>
                    </ListItemPrefix>
                    Logs
                </ListItem>

                <ListItem>
                    <ListItemPrefix>
                        <Cog6ToothIcon className="h-5 w-5"/>
                    </ListItemPrefix>
                    Settings
                </ListItem>

                <ListItem>
                    <ListItemPrefix>
                        <UserCircleIcon className="h-5 w-5"/>
                    </ListItemPrefix>
                    About
                </ListItem>
            </List>
        </Card>
    );
}