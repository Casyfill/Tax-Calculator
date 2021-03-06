from taxcalc import *

# use publicly-available CPS input file
recs = Records.cps_constructor()

# specify Calculator object representing current-law policy
pol = Policy()
calc1 = Calculator(policy=pol, records=recs)

cyr = 2020

# calculate aggregate current-law income tax liabilities for cyr
calc1.advance_to_year(cyr)
calc1.calc_all()
itax_rev1 = calc1.weighted_total('iitax')

# read JSON reform file and use (the default) static analysis assumptions
reform_filename = './ingredients/reformA.json'
params = Calculator.read_json_param_objects(reform=reform_filename,
                                            assump=None)

# specify Calculator object for static analysis of reform policy
pol.implement_reform(params['policy'])
calc2 = Calculator(policy=pol, records=recs)

# calculate reform income tax liabilities for cyr under static assumptions
calc2.advance_to_year(cyr)
calc2.calc_all()
itax_rev2 = calc2.weighted_total('iitax')

# read JSON reform file and (dynamic) behavioral-analysis assumptions
assump_filename = './ingredients/assumpA.json'
params = Calculator.read_json_param_objects(reform=reform_filename,
                                            assump=assump_filename)
behv = Behavior()
behv.update_behavior(params['behavior'])

# specify Calculator object for behavioral-response analysis of reform policy
calc3 = Calculator(policy=pol, records=recs, behavior=behv)

# calculate reform income tax liabilities for cyr under dynamic assumptions
calc3.advance_to_year(cyr)
calc3br = Behavior.response(calc1, calc3)
itax_rev3 = calc3br.weighted_total('iitax')

# print total revenue estimates for cyr
# (estimates in billons of dollars rounded to nearest hundredth of a billion)
print('{}_CURRENT_LAW_P__itax_rev($B)= {:.2f}'.format(cyr, itax_rev1 * 1e-9))
print('{}_REFORM_STATIC__itax_rev($B)= {:.2f}'.format(cyr, itax_rev2 * 1e-9))
print('{}_REFORM_DYNAMIC_itax_rev($B)= {:.2f}'.format(cyr, itax_rev3 * 1e-9))
