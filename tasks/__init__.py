def get_task(name, file=None):
    if name == 'trivia_creative_writing' or name == 'trivia_creative_writing_combine':
        from .trivia_creative_writing import TriviaCreativeWritingTask
        return TriviaCreativeWritingTask(file)
    elif name == 'logic_grid_puzzle' or name == 'logic_grid_puzzle_combine':
        from .logic_grid_puzzle import LogicGridPuzzleTask
        return LogicGridPuzzleTask(file)
    elif name == 'codenames_collaborative' or name == 'codenames_collaborative_combine':
        from .codenames_collaborative import CodenamesCollaborativeTask
        return CodenamesCollaborativeTask(file)
    elif name == 'grade_school_math' or name == 'grade_school_math_combine':
        from .grade_school_math import GradeSchoolMathTask
        return GradeSchoolMathTask(file)
    elif name =='massive_multitask_language_understanding' or name == 'massive_multitask_language_understanding_combine':
        from .massive_multitask_language_understanding import MMLUTask
        return MMLUTask(file)
    else:
        raise NotImplementedError