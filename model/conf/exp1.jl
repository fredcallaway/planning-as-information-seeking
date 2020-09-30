EXPERIMENT = "exp1"
COSTS = [0:0.05:4; 100]
MAX_THETA = 60
EXPAND_ONLY = true
FIT_BIAS = false

# QUOTE_MODELS = quote   # this quote thing allows us to refer to types that aren't defined yet
#     [
#         OptimalPlus{:Default},
#         MetaGreedy{:Default},
#         Heuristic{:Random},
#         Heuristic{:BestFirst},
#         Heuristic{:BestFirstNoPrune},
#         Heuristic{:BestFirstNoBestNext},
#     ]
# end

QUOTE_MODELS = quote 
    [
        OptimalPlus{:Default},
        MetaGreedy{:Default},
        Heuristic{:Random},
        Heuristic{:Best},
        Heuristic{:Best_Satisfice},
        Heuristic{:Best_BestNext},
        Heuristic{:Best_DepthLimit},
        Heuristic{:Best_Prune},
        Heuristic{:Best_Full},
        Heuristic{:Best_NoPrune},
        Heuristic{:Breadth_Full},
        Heuristic{:Depth_Full},
    ] 
end
        # Heuristic{:BestFirst},
        # Heuristic{:BestFirstSatisfice},
        # Heuristic{:BestFirstBestNext},
        # Heuristic{:BestFirstDepthLimit},
        # Heuristic{:BestFirstPrune},
        # Heuristic{:BestFirstFull},
        # Heuristic{:BestFirstNoPrune},
        # Heuristic{:BreadthFirstFull},
        # Heuristic{:DepthFirstFull},