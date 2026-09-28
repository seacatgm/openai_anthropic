%run -i gpu_fleet_review_out/calc_chips.py
cf = COEF.copy()
for c in ['server_w_per_chip', 'it_w_per_chip']: cf[c] = cf[c].round(0)
cf['h100e_per_chip'] = cf['h100e_per_chip'].round(3); cf['chips_per_gw_it'] = (cf['chips_per_gw_it'] / 1e3).round(0); cf['h100e_per_gw_it'] = (cf['h100e_per_gw_it'] / 1e3).round(0)
cf = cf.rename(columns={'chips_per_gw_it': 'тыс. чипов на 1 ГВт IT', 'h100e_per_gw_it': 'тыс. H100e на 1 ГВт IT'})
display(cf)
display(pd.DataFrame(R_CHIPS['control_points']).T)
