import re, json
B='/home/claude/'
# (fil, grupp, kort namn, [(radnr, rubrik, typ)], slutrad)  typ: I intro, L litteratur/teori/bakgrund, D data, M metod, DM data+metod, R resultat, X diskussion, B robusthet, C slutsats, H hypoteser
S=[
('raw/b07897b0-PETTENUZZO-CashFlowNews-2020.txt','sabb','JF 2020 Cash flow news',[(35,'Introduction (utan rubrik)','I'),(242,'I. Data','D'),(458,'II. Econometric Model','M'),(887,'III. Predictability of Dividend Growth','R'),(1802,'IV. Implications for Return Predictability','R'),(2477,'V. Dividend News and Return Dynamics','R'),(2775,'VI. Conclusion','C')],2837),
('raw/a4d9847a-Parsons-GeographicLeadLagEffects-2020.txt','sabb','RFS 2020 Geographic lead-lag',[(43,'Introduction (utan rubrik)','I'),(356,'1. Data and Descriptive Statistics','D'),(440,'2. Theoretical Motivation and Institutional Background','L'),(1611,'3. Lead-Lag Effects: Industry versus Regional Groups','R'),(2602,'4. Robustness and Extensions','B'),(3008,'5. Conclusions','C')],3148),
('raw/b559b3b6-rfae034.txt','sabb','RoF 2025 Tradable factors',[(30,'1. Introduction','I'),(254,'2. Data','D'),(521,'3. Constructing tradable risk factors','M'),(796,'4. Empirical results','R'),(1499,'5. Drivers of the implementation shortfall','R'),(3352,'6. Conclusion','C')],3857),
('raw/3abd8397-ssrn-3823258.txt','sabb','WP 2022 Payout suspensions',[(42,'1 Introduction','I'),(252,'2 Data','D'),(476,'3 The Value of Preserving Cash under Financial Distress','R'),(655,'4 Determinants of Payout Suspension Decisions','R'),(1083,'5 A Dynamic Test of the Pecking Order Theory','R'),(1302,'6 Conclusion','C')],1331),
('raw/e0979124-1-s2.0-S030440762300012X-main.txt','sabb','JoE 2023 Dividend suspensions',[(50,'1. Introduction','I'),(100,'2. Data','D'),(246,'3. A multivariate dividend growth model','M'),(1955,'4. Empirical results','R'),(2667,'5. Conclusion','C')],2678),
('raw/546a5877-1-s2.0-S0165176523000496-main.txt','sabb','EL 2023 Payout suspensions',[(45,'1. Introduction','I'),(78,'2. Data','D'),(149,'3. Dividend suspensions','R'),(234,'4. Buyback suspensions','R'),(397,'5. Conclusion','C')],430),
('top/hartzmark_sussman_2019.md','top','Hartzmark & Sussman 2019',[(106,'Introduction (utan rubrik)','I'),(173,'1 Sustainability Ratings','L'),(203,'2 Data Sources and Summary Statistics','D'),(225,'3 Do Investors Value Sustainability?','R'),(351,'4 Why do investors value sustainability?','R'),(473,'5 Conclusion','C')],493),
('top/bendavid_etal_2019wp.md','top','Ben-David et al. 2019 (arbetsversion)',[(34,'1 Introduction','I'),(200,'2 The Null Hypothesis','H'),(255,'3 Data and Measures','D'),(422,'4 Can BHO and BvB Reject the Null Hypothesis?','R'),(918,'5 How Do Investors Utilize Morningstar Ratings?','R'),(1140,'6 Conclusion','C')],1168),
('win/2019_per_hiller_tobins_q_and_filing_lag.txt','win','2019 PH',[(32,'1. Introduction','I'),(147,'2. Literature Review','L'),(291,'3. Data and Methodology','DM'),(535,'4. Results','R'),(704,'5. Implications and Conclusions','C')],735),
('win/2019_staffan_viotti_the_swedish_value_premium_and_disasters.txt','win','2019 SV',[(48,'1. Introduction','I'),(96,'2. Literature Review','L'),(214,'3. Data and methodology','DM'),(379,'4. Results','R'),(616,'5. Implications and Conclusions','C')],742),
('win/2020_per_hiller_chasing_your_own_tail.txt','win','2020 PH',[(41,'1. Introduction','I'),(158,'2. Theory, Practice and Literature Review','L'),(331,'3. Data','D'),(367,'4. LETF Rebalancing and the Market','R'),(458,'5. Flow-Induced Market Impact of LETFs','R'),(659,'6. Case Study: The Corona Crisis','R'),(704,'7. Price Impact and Market Microstructure Invariance','R'),(774,'8. Concluding Remarks','C')],829),
('win/2020_staffan_viotti_bank_stock_returns_and_monetary_policy_surprises.txt','win','2020 SV',[(22,'I. Introduction','I'),(124,'II. Literature review','L'),(181,'III. Methodology','M'),(365,'IV. Data description','D'),(409,'V. Empirical results','R'),(641,'VI. Interpretation of empirical findings','X'),(864,'VII. Conclusion','C')],891),
('win/2021_per_hiller_in_the_eye_of_a_pandemic.txt','win','2021 PH',[(43,'1. Introduction','I'),(131,'2. Theoretical Framework & Literature Review','L'),(288,'3. Hypotheses','H'),(373,'4. Data','D'),(614,'5. Methodology','M'),(691,'6. Empirical Results','R'),(836,'7. Discussion','X'),(1048,'8. Concluding Remarks','C')],1131),
('win/2021_staffan_viotti_market_microstructure_invariance.txt','win','2021 SV',[(40,'Introduction','I'),(130,'1. Fundamental Concepts','L'),(193,'2. Literature Review','L'),(242,'3. Theoretical Background','L'),(496,'4. Hypotheses and Research Design','H'),(646,'5. Data','D'),(861,'6. Empirical Findings','R'),(1046,'7. Concluding Remarks','C')],1095),
('win/2022_per_hiller_predicting_liquidity_in_cryptocurrency_market.txt','win','2022 PH',[(38,'I. Introduction','I'),(138,'II. Fundamental Concepts','L'),(212,'III. Literature Review','L'),(251,'IV. Theoretical Background','L'),(433,'V. Hypotheses and Research Design','H'),(507,'VI. Data','D'),(749,'VII. Empirical findings','R'),(851,'VIII. Concluding remarks','C')],881),
('win/2022_staffan_viotti_owning_the_wave.txt','win','2022 SV',[(37,'I. Introduction','I'),(152,'II. Theoretical Background','L'),(199,'III. Data','D'),(300,'IV. Empirical Results and Analysis','R'),(516,'V. Robustness Checks','B'),(536,'VI. Conclusion','C')],552),
('win/2023_per_hiller_changing_patterns_over_the_fomc_cycle.txt','win','2023 PH',[(38,'I. Introduction','I'),(175,'II. Theoretical Framework','L'),(222,'III. Data Description and Methodology','DM'),(356,'IV. Analysis and Results','R'),(569,'V. Discussion','X'),(733,'VI. Conclusion','C')],768),
('win/2023_staffan_viotti_the_drivers_of_wealth_inequality.txt','win','2023 SV',[(33,'1 Introduction','I'),(105,'2 Related Works','L'),(142,'3 Wealth Model','M'),(302,'4 Model Estimation','DM'),(448,'5 Results','R'),(586,'6 Robustness','B'),(637,'7 Conclusion','C')],707),
('win/2024_per_hiller_the_smooth_transition.txt','win','2024 PH',[(39,'1 Introduction','I'),(184,'2 Data and Methodology','DM'),(473,'3 Results','R'),(548,'4 Discussion','X'),(681,'5 Conclusion','C')],702),
('win/2025_unofficial_6338_leading_the_wallet.txt','win','2025 (inofficiell)',[(41,'I. Introduction','I'),(185,'II. Conceptual Framework','L'),(290,'III. Data Sources and Description','D'),(548,'IV. Methodology and Results','R'),(1134,'V. Robustness Check','B'),(1237,'VI. Conclusion','C')],1281),
]
def words(lines):
    t=' '.join(lines)
    return len(re.findall(r"[A-Za-z][A-Za-z’'\-]+",t))
out=[]
for fil,grp,namn,sek,slut in S:
    L=open(B+fil,encoding='utf-8',errors='ignore').read().split('\n')
    rows=[]
    for i,(r,rub,typ) in enumerate(sek):
        nxt=sek[i+1][0] if i+1<len(sek) else slut
        rows.append((rub,typ,words(L[r-1:nxt-1])))
    tot=sum(w for _,_,w in rows)
    ag={}
    for rub,typ,w in rows: ag[typ]=ag.get(typ,0)+w
    out.append(dict(namn=namn,grp=grp,n=len(rows),tot=tot,ordning=' '.join(t for _,t,_ in rows),andel={k:round(100*v/tot,1) for k,v in ag.items()},rader=[(rub,typ,w,round(100*w/tot,1)) for rub,typ,w in rows]))
json.dump(out,open('struktur.json','w'),ensure_ascii=False,indent=1)
for o in out:
    print(f"\n{o['namn']} [{o['grp']}] sektioner={o['n']} ord={o['tot']} ordning={o['ordning']}")
    for rub,typ,w,a in o['rader']: print(f"   {a:5.1f}%  {w:6d}  {typ:2s} {rub}")
import statistics as st
def med(grp,key):
    v=[o['andel'].get(key,0) for o in out if o['grp']==grp]
    return st.median(v), min(v), max(v), sum(1 for x in v if x>0), len(v)
print()
for grp in ('sabb','top','win'):
    print(grp, 'antal sektioner median', st.median([o['n'] for o in out if o['grp']==grp]))
    for key in ('I','L','H','D','M','DM','R','X','B','C'):
        m,a,b,k,n=med(grp,key); print(f"   {key:2s} median {m:5.1f}  min {a:5.1f} max {b:5.1f}  finns i {k}/{n}")
