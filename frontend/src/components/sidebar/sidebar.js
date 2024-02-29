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

import {Link} from 'react-router-dom';

export function DefaultSidebar() {
    return (
        <Card className="h-[calc(100vh-2rem)] w-full max-w-[20rem] p-4 shadow-xl shadow-blue-gray-900/5">
            <List>
                <Link to="/">
                    <ListItem>
                        <ListItemPrefix>
                            <PresentationChartBarIcon className="h-5 w-5"/>
                        </ListItemPrefix>
                        Logs
                    </ListItem>
                </Link>

                <Link to="/settings">
                    <ListItem>
                        <ListItemPrefix>
                            <Cog6ToothIcon className="h-5 w-5"/>
                        </ListItemPrefix>
                        Settings
                    </ListItem>
                </Link>

                <Link to="/about">
                    <ListItem>
                        <ListItemPrefix>
                            <UserCircleIcon className="h-5 w-5"/>
                        </ListItemPrefix>
                        About
                    </ListItem>
                </Link>
            </List>
        </Card>
    );
}