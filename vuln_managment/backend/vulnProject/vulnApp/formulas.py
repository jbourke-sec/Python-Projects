class formulas():
    def environmentalScore(mis, scope, impact, exploitability, ecm, rl, rc):
        ecmb = 0
        rlb = 0
        rcb = 0
        if ecm == 'Not Defined':
            ecmb = 1
        if ecm == 'Functional exploit exists':
            ecmb = 0.95
        elif ecm == 'Proof of concept code':
            ecmb = 0.9
        elif ecm == 'Unproven that exploit exists':
            ecmb = 0.85
        if rl == 'Unavailable' or rl == 'Not Defined':
            rlb = 1
        elif rl == 'Workaround':
            rlb = 0.97
        elif rl == 'Temporary fix':
            rlb = 0.96
        elif rl == 'Official fix':
            rlb = 0.95
        if rc == 'Unknown':
            rcb = 0.92
        elif rc == 'Reasonable':
            rcb = 0.96
        elif rc == 'Confirmed' or rc == 'Not Defined':
            rcb = 1
        print('enscore')
        print(mis, impact, exploitability, ecmb, rlb, rcb)
        if mis <= 0:
            return 0
        elif scope == 'Unchanged':
            return round(round(min(1.08 * (impact + exploitability), 10) * ecmb * rlb * rcb, 1), 1)
        elif scope == 'Changed' or scope == 'Not Defined':
            return round(round(min((impact + exploitability), 10) * ecmb * rlb * rcb, 1), 1)
    def impactModScore(mis, scope):
        if scope == 'Unchanged':
            return 6.42 * mis
        if scope == 'Changed' or scope == 'Not Defined':
            return (7.52 * (mis - 0.029)-3.25 * (mis * 0.9731 - 0.02)**13)
    def impactScore(mis, scope):
        if scope == 'Unchanged':
            return 6.42 * mis
        elif scope == 'Changed' or scope == 'Not Defined':
            return 7.52 * (mis - 0.029) - 3.25 * (mis - 0.02)**15
    def iscmodified(conf, integ, avail, confreq, intreq, availreq):
        confb = 0
        integb = 0
        availb = 0
        confreqb = 0
        intreqb = 0
        availreqb = 0
        if intreq == 'Low Requirement':
            intreqb = 0.51
        if confreq == 'Low Requirement':
            confreqb = 0.51
        if availreq == 'Low Requirement':
            availreqb = 0.51
        if intreq == 'Not Defined' or intreq == 'Medium Requirement':
            intreqb = 1
        if confreq == 'Not Defined' or confreq == 'Medium Requirement':
            confreqb = 1
        if availreq == 'Not Defined' or availreq == 'Medium Requirement':
            availreqb = 1
        if intreqb == 'High Requirement':
            intreqb = 1.51
        if availreq == 'High Requirement':
            availreqb = 1.51
        if availreq == 'High Requirement':
            availreqb = 1.51

        if conf == 'High':
            confb = 0.56
        if conf == 'Low':
            confb = 0.22
        if conf == 'None':
            confb = 0
        if integ == 'High':
            integb = 0.56
        if integb == 'Low':
            integb = 0.22
        if integ == 'None':
            integb = 0
        if avail == 'High':
            availb = 0.56
        if avail == 'Low':
            availb = 0.22
        if avail == 'None':
            availb = 0
        return min(((1 - (1 - confb * confreqb) * (1 - integb * intreqb) * (1 - availb * availreqb)), 0.915))
    def exploitScore(av,ac, pr, ui, scope):
        bac = 0
        bac = 0
        bpr = 0
        bui = 0
        if av == 'Network':
            bav = 0.85
        elif av == 'Adjacent Network':
            bav = 0.62
        elif av == 'Local':
            bav = 0.55
        elif av == 'Physical':
            bav = 0.22
        if ac == 'High':
            bac = 0.44
        elif ac == 'Low':
            bac = 0.77
        elif ac == 'Not Defined':
            bac = 0.77
        if pr == 'High' and scope == 'Changed':
            bpr = 0.5
        elif pr == 'High' and scope == 'Unchanged':
            bpr = 0.27
        elif pr == 'Low' and scope == 'Changed':
            bpr = 0.68
        elif pr == 'Low' and scope == 'Unchanged':
            bpr = 0.62
        elif pr == 'None':
            bpr = 0.85
        if ui == 'Required':
            bui = 0.62
        elif ui == 'None' or ui == 'Not Defined':
            bui = 0.85
        return (8.22 * bav * bac * bpr * bui)
    def temporal(bs, ecm, rl, rc):
        ecmb = 0
        rlb = 0
        rcb = 0
        if ecm == 'Not Defined':
            ecmb = 1
        if ecm == 'Functional exploit exists':
            ecmb = 0.95
        elif ecm == 'Proof of concept code':
            ecmb = 0.9
        elif ecm == 'Unproven that exploit exists':
            ecmb = 0.85
        if rl == 'Unavailable' or rl == 'Not Defined':
            rlb = 1
        elif rl == 'Workaround':
            rlb = 0.97
        elif rl == 'Temporary fix':
            rlb = 0.96
        elif rl == 'Official fix':
            rlb = 0.95
        if rc == 'Unknown':
            rcb = 0.92
        elif rc == 'Reasonable':
            rcb = 0.96
        elif rc == 'Confirmed' or rc == 'Not Defined':
            rcb = 1
        return round(bs * ecmb * rlb * rcb, 1)
    def iscbase(conf, avail, integ):
        confb = 0
        integb = 0
        availb = 0
        if conf == 'High':
            confb = 0.56
        if conf == 'Low':
            confb = 0.22
        if conf == 'None':
            confb = 0
        if integ == 'High':
            integb = 0.56
        if integ == 'Low':
            integb = 0.22
        if integ == 'None':
            integb = 0
        if avail == 'High':
            availb = 0.56
        if avail == 'Low':
            availb = 0.22
        if avail == 'None':
            availb = 0
        return (1-((1-confb)*(1 - integb)*(1 - availb)))
    def baseScore(iss, scope, impact, exploitability):
        if iss <= 0:
            return 0
        if scope == 'Unchanged':
            return round(min((impact + exploitability), 10), 1)
        elif scope == 'Changed' or scope == 'Not Defined':
            return round(min((1.08 * impact + exploitability), 10), 1)