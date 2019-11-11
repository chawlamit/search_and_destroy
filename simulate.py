from terrain import Terrain
from environment import Environment
from agents.bayesian_agent_rule1 import BayesianAgentRule1
from agents.bayesian_agent_rule2 import BayesianAgentRule2
from agents.min_action_agent import MinActionAgent
from multiprocessing import Process, Pool
from sample_env import sample_env

env = Environment(50)
env.generate_from_sample(sample_env)
# env.show()


def simulate(agent_holder):
    n_sims = 1
    search_count_list = []
    travel_count_list = []
    for i in range(n_sims):
        terrain = "flat"
        env.place_target(terrain=terrain)
        print(f"Agent : {agent_holder.__name__}, terrain: {env.get_terrain(*env.target)}, Target: {env.target}, ")
        agent = agent_holder(env)
        agent.run()
        search_count_list.append(agent.search_count)
        travel_count_list.append(agent.travel_count)
        print(f"Agent : {agent_holder.__name__}, Terrain {terrain}, Iteration:{i}, Search Count:{agent.search_count}, "
              + f"Travel count:{agent.travel_count}")

    print(f'Total - Agent : {agent_holder.__name__}, Search_count:{search_count_list}, Travel_count:{travel_count_list}')


if __name__ == "__main__":
    agents_list = [BayesianAgentRule1, BayesianAgentRule2, MinActionAgent]
    pool = Pool(processes=3)
    pool.map(simulate, agents_list)

