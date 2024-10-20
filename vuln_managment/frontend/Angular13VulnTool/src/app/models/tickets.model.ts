import { Time } from "@angular/common";
import { Assets } from "./assets.model";
import { Playbook } from "./playbook.model";
import { Vulnerability } from "./vulnerability.model";

export class Tickets {

    ticketNumber?: any;
    summary?: string;
    validatedsummary?: string;
    verifiedsummary?: string;
    rolledsummary?: string;
    progress?: string;
    assignedTo?: string;
    group?: string;
    timeStarted?: string;
    timeClosed?: any;
    cve?: string;
    vulnid?: Vulnerability;
    cvss?: string;
    qa?: string;
    sla?: any;
    exposure?: string;
    threat?: string;
    assets?: Assets[];
    outcome?: string;
    playbookid?: Playbook;
    acquired?: boolean;
    validated?: boolean;
    verified?: boolean;
    rolledout?: boolean;
    enscore?: any;
    iscbase?: any;
    temporal?: any;
    exploitScore: any;
    iscmodified: any;
    impactModScore: any;
    impactScore: any;
    environmentalScore: any;
}
