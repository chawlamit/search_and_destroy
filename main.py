from environment import Environment
from agents.bayesian_agent_rule1 import BayesianAgentRule1
from agents.bayesian_agent_rule2 import BayesianAgentRule2
from agents.min_action_agent import MinActionAgent

env = Environment(10, place_target_in="flat")
print(f"Target: {env.target}, terrain: {env.get_terrain(*env.target)}")
# env.show()


# agent = BayesianAgentRule1(env, visualize=True)
# agent.run()
# print(f"{agent.__class__}: Search Count - {agent.search_count}, Total Actions - {agent.total_actions()}")
#
agent = BayesianAgentRule2(env, visualize=True)
agent.run()
print(f"{agent.__class__}: Search Count - {agent.search_count}, Total Actions - {agent.total_actions()}")
# #
# agent = MinActionAgent(env, visualize=True)
# agent.run()
# print(f"{agent.__class__}: Search Count - {agent.search_count}, Total Actions - {agent.total_actions()}")