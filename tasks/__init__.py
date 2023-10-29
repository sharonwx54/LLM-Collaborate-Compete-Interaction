def get_task(name, file=None):
    if name == 'trivia_creative_writing':
        from .trivia_creative_writing import TriviaCreativeWritingTask
        return TriviaCreativeWritingTask(file)
    elif name == 'logic_grid_puzzle':
        from .logic_grid_puzzle import LogicGridPuzzleTask
        return LogicGridPuzzleTask(file)
    elif name == 'codenames_collaborative':
        from .codenames_collaborative import CodenamesCollaborativeTask
        return CodenamesCollaborativeTask(file)
    elif name == 'grade_school_math':
        from .grade_school_math import GradeSchoolMathTask
        return GradeSchoolMathTask(file)
    elif name =='massive_multitask_language_understanding':
        from .massive_multitask_language_understanding import MMLUTask
        return MMLUTask(file)
    else:
        raise NotImplementedError