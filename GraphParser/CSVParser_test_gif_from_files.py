# Set up_to_number to be as the last file's name.
# Example 086.jpg -> 86
up_to_number = 86
filenames = []

for i in range(0, up_to_number+1):
    filename = "".join(["images/", format(i, '03'), ".jpg"])
    filenames.append(filename)


print filenames


# now save them to gif
frames = 0
import imageio
with imageio.get_writer('animation_.gif', mode='I') as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)
        frames += 1

print "Saved to animation.gif with <", frames, "> frames."

