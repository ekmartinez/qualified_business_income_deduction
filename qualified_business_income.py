

class Qbi:
    def __init__(self, status, b_type, taxable_income, qbi, w2_wages, qualified_property, capital_gains):
        self.b_type = b_type
        self.status = status
        self.taxable_income = taxable_income
        self.qbi = qbi
        self.w2_wages = w2_wages
        self.qualified_property = qualified_property
        self.capital_gains = capital_gains

        self.QBI_PCT = .20
        self.thresholds = {'Single' : [164900, 214900], 'Married' : [329800, 429800]}

    def qtb_single_below(self):
        tentative_qbi = self.qbi * self.QBI_PCT
        taxable_income_over_capital_gains = (self.taxable_income - self.capital_gains) * self.QBI_PCT
        return min(tentative_qbi, taxable_income_over_capital_gains)

    def qtb_single_between(self):
        tentative_qbi = self.qbi * self.QBI_PCT
        
        #W-2 Wage and Property Limitation - Greater of (a) 50% W2 or (b) 25% W2 + 2.5% basis qualified property
        a = self.w2_wages * .50
        b = (self.w2_wages * .25) + (self.qualified_property * .025)
        limitation = max(a, b)

        #Phase In Percentage
        phase_in = (self.taxable_income - self.thresholds['Single'][0]) / 50000

        allowed_qbi = tentative_qbi - (tentative_qbi - limitation) * phase_in
        taxable_income_over_capital_gains = (self.taxable_income - self.capital_gains) * self.QBI_PCT
        return min(allowed_qbi, taxable_income_over_capital_gains)

    def qtb_single_above(self):
        tentative_qbi = self.qbi * self.QBI_PCT

        #W-2 Wage and Property Limitation - (a) Greater of 50% W2 or (b) 25% W2 + 2.5% basis qualified property
        a = self.w2_wages * .50
        b = (self.w2_wages * .25) + (self.qualified_property * .025)
        limitation = max(a, b)

        allowed_qbi = min(tentative_qbi, limitation)
        taxable_income_over_capital_gains = (self.taxable_income - self.capital_gains) * self.QBI_PCT
        return min(allowed_qbi, taxable_income_over_capital_gains)

    def sstb_single_below(self):
        tentative_qbi = self.qbi * self.QBI_PCT
        taxable_income_over_capital_gains = (self.taxable_income - self.capital_gains) * self.QBI_PCT
        return min(tentative_qbi, taxable_income_over_capital_gains)

    def sstb_single_between(self):
        #TODO: Compute for sstb
        pass
    
    def sstb_single_above(self):
        return 0

    def runner(self):
            if self.b_type.lower() == 'qtb' and self.status.lower() == 'single' \
                and self.taxable_income <= self.thresholds['Single'][0]:
                return f'\nResults\n{"-"*30}\nQbi Deduction = {self.qtb_single_below():,.2f}\n{"-"*30}\n'

            elif self.b_type.lower() == 'qtb' and self.status.lower() == 'single' \
                and self.taxable_income >= self.thresholds['Single'][0] and self.taxable_income <= self.thresholds['Single'][1]:
                return f'\nResults\n{"-"*30}\nQbi Deduction = {self.qtb_single_between():,.2f}\n{"-"*30}\n'

            elif self.b_type.lower() == 'qtb' and self.status.lower() == 'single' \
                and self.taxable_income >= self.thresholds['Single'][1]:
                return f'\nResults\n{"-"*30}\nQbi Deduction = {self.qtb_single_above():,.2f}\n{"-"*30}\n'