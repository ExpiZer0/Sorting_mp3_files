import os

import click
import eyed3


@click.command()
@click.option('-s', '--src-dir', default=os.getcwd(), help='Source directory.')
@click.option('-d', '--dst-dir', default=os.getcwd(), help='Destination directory.')
def run(src_dir, dst_dir):
    """Sort start if no errors"""

    try:
        os.chdir(src_dir)
    except NotADirectoryError:
        print('A directory was expected, but a file was specified.')
    except FileNotFoundError:
        print('Source directory does not exist.')
    else:
        try:
            os.chdir(dst_dir)
        except FileNotFoundError:
            print('Destination directory does not exist. A directory will be created.')
            os.makedirs(dst_dir, mode=0o777, exist_ok=True)
        finally:
            sorting(src_dir, dst_dir)


def sorting(src_dir, dst_dir):
    """Sorting code"""

    src_path = src_dir
    dst_path = dst_dir
    access = True

    for filename in os.listdir(src_path):
        path = os.path.join(src_path, filename)
        if os.path.isfile(path):
            if filename[-1:-4:-1] == '3pm':
                # Creation dst path

                addfile = eyed3.load(path)
                if addfile.tag.artist is None or addfile.tag.album is None:
                    print(f'The file {filename} does not have enough information. He will not be moved.')
                    continue
                elif addfile.tag.title is None:
                    new_path = os.path.join(dst_path, f'{addfile.tag.artist}', f'{addfile.tag.album}', f'{filename}')
                else:
                    new_path = os.path.join(dst_path, f'{addfile.tag.artist}', f'{addfile.tag.album}',
                                            f'{addfile.tag.title} - {addfile.tag.artist} - {addfile.tag.album}.mp3')

                try:
                    os.renames(path, new_path)
                except FileExistsError:
                    os.replace(path, new_path)
                except PermissionError:
                    print('Access violation!')
                    access = False
                finally:
                    if access:
                        print(path, ' -> ', new_path)
                    access = True

    print('Done.')


if __name__ == '__main__':
    run()
