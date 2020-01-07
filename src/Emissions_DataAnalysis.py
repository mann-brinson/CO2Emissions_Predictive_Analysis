import gdp_cleaning
import realgdp_cleaning
import incomepop_cleaning
import emissions_cleaning
import emissions_by_sector_cleaning
import energyprod_cleaning
import energyconsumption_cleaning
import emissions_regressions
import decisiontree_emis_allfuels
import decisiontree_emis_fossilfuels
import decisiontree_transemis_fossilfuels
import sys

print(f"We're in file {__file__}")

#Require the user to input this driver and source option
#Will prompt the user to enter a source argument (remote or local)
if len(sys.argv) < 2:
    print('To few arguments, please put in Emissions_DataAnalysis.py and data source argument (remote or local). EX: "Emissions_DataAnalysis.py remote"')
    sys.exit(0)

if sys.argv[1] == 'remote':
	print("Calling gdp_cleaning.py...")
	gdp_cleaning.main()
	print("Calling realgdp_cleaning.py...")
	realgdp_cleaning.main()
	print("Calling incomepop_cleaning.py...")
	incomepop_cleaning.main()
	print("Calling emissions_cleaning.py...")
	emissions_cleaning.main()
	print("Calling emissions_by_sector_cleaning.py...")
	emissions_by_sector_cleaning.main()
	print("Calling energyprod_cleaning.py...")
	energyprod_cleaning.main()
	print("Calling energyconsumption_cleaning.py...")
	energyconsumption_cleaning.main()
	print("Calling emissions_regressions.py...")
	emissions_regressions.main()
	print("Calling decisiontree_emis_allfuels.py...")
	decisiontree_emis_allfuels.main()
	print("Calling decisiontree_emis_fossilfuels.py...")
	decisiontree_emis_fossilfuels.main()
	print("Calling decisiontree_transemis_fossilfuels.py...")
	decisiontree_transemis_fossilfuels.main()

elif sys.argv[1] == 'local':
	print("Calling emissions_regressions.py...")
	emissions_regressions.main()
	print("Calling decisiontree_emis_allfuels.py...")
	decisiontree_emis_allfuels.main()
	print("Calling decisiontree_emis_fossilfuels.py...")
	decisiontree_emis_fossilfuels.main()
	print("Calling decisiontree_transemis_fossilfuels.py...")
	decisiontree_transemis_fossilfuels.main()

else:
	print("Please enter 'remote' or 'local' as your second argument. EX: 'MANN_MARK_hw5.py remote' ")
	sys.exit(0)
